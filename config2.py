import subprocess
import sys
import os
import json
import argparse

def get_dependencies(package_name, repo_url):
    # Клонируем репозиторий
    subprocess.run(['git', 'clone', repo_url], check=True)

    # Переходим в директорию с репозиторием
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    os.chdir(repo_name)

    # Запускаем npm install для установки зависимостей
    subprocess.run(['npm', 'install'], check=True)

    # Получаем зависимости из package.json
    with open('package.json', 'r') as file:
        package_data = json.load(file)
    
    dependencies = package_data.get('dependencies', {})
    return dependencies

def generate_plantuml(dependencies):
    plantuml_string = '@startuml\n'
    
    for dep, version in dependencies.items():
        plantuml_string += f'"{dep}" --> "{version}"\n'
    
    plantuml_string += '@enduml\n'
    return plantuml_string

def main():
    parser = argparse.ArgumentParser(description='Visualize dependency graph of a JavaScript package.')
    parser.add_argument('visualizer_path', type=str, help='Path to the PlantUML visualizer')
    parser.add_argument('package_name', type=str, help='Name of the package to analyze')
    parser.add_argument('repo_url', type=str, help='URL of the repository')

    args = parser.parse_args()

    dependencies = get_dependencies(args.package_name, args.repo_url)
    plantuml_content = generate_plantuml(dependencies)

    # Сохраняем содержание PlantUML в файл
    with open('dependencies.puml', 'w') as file:
        file.write(plantuml_content)

    # Запускаем PlantUML для генерации графика
    #subprocess.run([args.visualizer_path, 'dependencies.puml'])
    subprocess.run(['java', '-jar', args.visualizer_path, 'dependencies.puml'])

if __name__ == "__main__":
    main()

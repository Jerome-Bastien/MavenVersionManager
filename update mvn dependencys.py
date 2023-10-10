import os
import re
import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET

XML_NAMESPACE = "http://maven.apache.org/POM/4.0.0"

project_dir_path = r"C:\Users\JerBa\Desktop\synka\PDFUtil\Java\eclipse-workspace"
group_ids_path = r"C:\Users\JerBa\Desktop\synka\PDFUtil\Java\eclipse-workspace\VersionManagment\group_ids.txt"
repository_path = r"C:\\Users\\JerBa\\.m2\\repository"

label = None

def update_dependency_version(xml_path, group_id, artifact_id, new_version):
    try:
        namespaces = {"ns": "http://maven.apache.org/POM/4.0.0"}
        tree = ET.parse(xml_path)
        root = tree.getroot()

        dependency_elem = None
        for dependency in root.findall(".//ns:dependencies/ns:dependency", namespaces):
            dep_group_id = dependency.find("ns:groupId", namespaces).text
            dep_artifact_id = dependency.find("ns:artifactId", namespaces).text
            if dep_group_id == group_id and dep_artifact_id == artifact_id:
                dependency_elem = dependency
                break

        if dependency_elem is not None:
            version_elem = dependency_elem.find("ns:version", namespaces)
            if version_elem is None:
                version_elem = ET.Element(f"{{ns}}version")
                dependency_elem.append(version_elem)
            version_elem.text = new_version

            ET.register_namespace('', XML_NAMESPACE)
            tree.write(xml_path, encoding="utf-8", xml_declaration=True, default_namespace=XML_NAMESPACE)
            print(f"Updated version of {group_id}:{artifact_id} to {new_version} in {xml_path}")
        else:
            print(f"Dependency {group_id}:{artifact_id} not found in {xml_path}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")


def update_dependencies_in_directory(directory_path, group_id, artifact_id, new_version):
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename == "pom.xml":
                pom_xml_path = os.path.join(root, filename)
                update_dependency_version(pom_xml_path, group_id, artifact_id, new_version)


def open_window(available_group_ids, available_artifact_ids, available_versions):
    def on_combobox_change(event):
        combobox = event.widget

        if combobox == group_id_combobox:
            selected_group = group_id_combobox.get()
            artifact_ids = get_artifact_ids(repository_path, selected_group)
            artifact_id_combobox["values"] = artifact_ids
            artifact_id_combobox.set(artifact_ids[0])

            available_artifact_ids.clear()
            available_artifact_ids.extend(artifact_ids)

        if combobox == group_id_combobox or combobox == artifact_id_combobox:
            versions = get_versions(r"C:\Users\JerBa\.m2\repository", group_id_combobox.get(),
                                    artifact_id_combobox.get())
            version_combobox["values"] = versions

            available_versions.clear()
            available_versions.extend(versions)

        version_combobox.set(available_versions[len(available_versions) - 1])

    window = tk.Tk()
    window.title("Update Maven Dependencies")

    window.geometry("400x180")

    tk.Label(window, text="Directory Path:").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="e")
    directory_path_entry = tk.Entry(window, width=40)
    directory_path_entry.grid(row=0, column=1, padx=10, pady=(10, 0))
    directory_path_entry.insert(0, project_dir_path)

    tk.Label(window, text="Group ID:").grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")
    group_id_combobox = ttk.Combobox(window, width=37, values=available_group_ids)
    group_id_combobox.grid(row=1, column=1, padx=10, pady=(10, 0))

    group_id_combobox.bind("<<ComboboxSelected>>", on_combobox_change)
    tk.Label(window, text="Artifact ID:").grid(row=2, column=0, padx=10, pady=(10, 0), sticky="e")
    artifact_id_combobox = ttk.Combobox(window, width=37, values=available_artifact_ids)
    artifact_id_combobox.grid(row=2, column=1, padx=10, pady=(10, 0))
    artifact_id_combobox.bind("<<ComboboxSelected>>", on_combobox_change)

    tk.Label(window, text="Version:").grid(row=3, column=0, padx=10, pady=(10, 0), sticky="e")
    version_combobox = ttk.Combobox(window, width=37, values=available_versions)
    version_combobox.grid(row=3, column=1, padx=10, pady=(10, 0))

    def submit():
        directory_path = directory_path_entry.get()
        group_id = group_id_combobox.get()
        artifact_id = artifact_id_combobox.get()
        version = version_combobox.get()

        update_dependencies_in_directory(directory_path, group_id, artifact_id, version)

    submit_button = tk.Button(window, text="Submit", command=submit)
    submit_button.grid(row=4, column=1, padx=5, pady=(5, 5), sticky="e")

    if len(available_artifact_ids) > 0:
        artifact_id_combobox.set(available_artifact_ids[0])

    if len(available_group_ids) > 0:
        group_id_combobox.set(available_group_ids[0])

    if len(available_versions) > 0:
        version_combobox.set(available_versions[len(available_versions) - 1])

    window.mainloop()


def get_artifact_ids(m2_repository_path, group_id):
    artifact_ids = []

    group_id_path = os.path.join(m2_repository_path, group_id.replace('.', os.path.sep))

    if os.path.exists(group_id_path):
        for entry in os.scandir(group_id_path):
            if entry.is_dir():
                artifact_id = entry.name
                artifact_ids.append(artifact_id)

    return artifact_ids


def get_versions(directory, group_id, artifact_id):
    versions = []

    # Construct the directory path for the given group_id and artifact_id
    group_id_path = group_id.replace('.', '/')
    artifact_path = os.path.join(directory, group_id_path, artifact_id)

    # Check if the artifact directory exists
    if not os.path.exists(artifact_path):
        print(f"No versions found for group_id '{group_id}' and artifact_id '{artifact_id}'.")
        return versions

    # Iterate through the subdirectories (versions) and collect versions
    for version in os.listdir(artifact_path):
        version_path = os.path.join(artifact_path, version)
        if os.path.isdir(version_path):
            versions.append(version)

    return versions


def read_file_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        return lines
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


if __name__ == "__main__":
    group_ids = read_file_lines(group_ids_path)
    artifact_ids = get_artifact_ids(repository_path, group_ids[0])
    versions = get_versions(repository_path, group_ids[0], artifact_ids[0])

    open_window(group_ids, artifact_ids, versions)

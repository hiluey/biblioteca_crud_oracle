import subprocess 

subprocess.run("cd src && python create_tables_biblioteca.py && python principal.py", shell=True, check=True)
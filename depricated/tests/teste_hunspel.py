import subprocess

# Palavra a verificar
word = "casaa"

# Chama o hunspell do sistema
proc = subprocess.Popen(
    ['hunspell', '-d', 'pt_BR', '-a'],  # -a modo pipe para script
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Envia a palavra
stdout, stderr = proc.communicate(input=f"{word}\n".encode())

# Decodifica a saída
output = stdout.decode()
print(output)

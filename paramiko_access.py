import paramiko
import getpass

# Функция для подключения к удаленному серверу и выполнения команд
def create_ansible_user(hostname, username, password):
    try:
        # Создание SSH-клиента
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Подключение к серверу
        client.connect(hostname, username=username, password=password)

        # Команды для создания пользователя ansible и настройки его SSH-доступа
        commands = [
            "sudo useradd -m ansible",
            "echo 'ansible:password' | sudo chpasswd",  # Установка пароля для пользователя ansible
            "sudo mkdir /home/ansible/.ssh",
            "sudo chown ansible:ansible /home/ansible/.ssh",
            "sudo chmod 700 /home/ansible/.ssh"
        ]

        # Выполнение команд на удаленном сервере
        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            stdin.write(password + "\n")  # Для sudo
            stdin.flush()
            print(f"Command: {command}")
            print(f"Output: {stdout.read().decode()}")
            print(f"Error: {stderr.read().decode()}")

        # Здесь вместо your_public_key необходимо указать путь к вашему публичному ключу
        public_key_path = 'path_to_your_public_key.pub'
        with open(public_key_path, 'r') as f:
            public_key = f.read()

        # Команда для добавления ключа в authorized_keys
        command_add_key = "echo '{}' | sudo tee -a /home/ansible/.ssh/authorized_keys".format(public_key)
        stdin, stdout, stderr = client.exec_command(command_add_key)
        stdin.write(password + "\n")  # Для sudo
        stdin.flush()

        print(f"Output: {stdout.read().decode()}")
        print(f"Error: {stderr.read().decode()}")

        # Изменение прав на файлы
        commands_permissions = [
            "sudo chown ansible:ansible /home/ansible/.ssh/authorized_keys",
            "sudo chmod 600 /home/ansible/.ssh/authorized_keys"
        ]

        for command in commands_permissions:
            stdin, stdout, stderr = client.exec_command(command)
            stdin.write(password + "\n")  # Для sudo
            stdin.flush()
            print(f"Command: {command}")
            print(f"Output: {stdout.read().decode()}")
            print(f"Error: {stderr.read().decode()}")

        print(f"User 'ansible' created and SSH keys set for {hostname}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    # Указываем удалённые серверы и их учетные данные
    host = input("Enter the host IP or hostname: ")
    user = input("Enter your SSH username: ")
    password = getpass.getpass("Enter your SSH password: ")

    create_ansible_user(host, user, password)

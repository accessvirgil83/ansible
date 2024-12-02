#!/bin/bash

# Запросить информацию у пользователя
read -p "Enter the host IP or hostname: " host
read -p "Enter your SSH username: " user
# Используем скрытый ввод для пароля
read -s -p "Enter your SSH password: " password
echo
# Пароль для нового пользователя ansible
ansible_password="password"

# Выполнение команд на удаленном сервере
sshpass -p "$password" ssh -o StrictHostKeyChecking=no "$user@$host" bash << EOF
    # Создание пользователя ansible
    sudo -i useradd -m ansible

    # Установка пароля для пользователя ansible
    echo "ansible:$ansible_password" | sudo -i chpasswd

    # Настройка SSH-доступа для пользователя ansible
    sudo -i mkdir /home/ansible/.ssh
    sudo -i chown ansible:ansible /home/ansible/.ssh
    sudo -i chmod 700 /home/ansible/.ssh

    # Здесь укажите путь к вашему публичному ключу
    public_key_path='/path/to/your/public_key.pub'
    if [ -f "\$public_key_path" ]; then
        # Добавление SSH-ключа в authorized_keys
        cat "\$public_key_path" | sudo -i tee -a /home/ansible/.ssh/authorized_keys
        sudo -i chown ansible:ansible /home/ansible/.ssh/authorized_keys
        sudo -i chmod 600 /home/ansible/.ssh/authorized_keys
    else
        echo "Public key file not found: \$public_key_path"
    fi

    echo "User 'ansible' created and SSH keys set for $host"
EOF

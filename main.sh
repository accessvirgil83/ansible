#!/bin/bash

# Обновление списка пакетов
echo "Updating package list..."
apt update -y

# Установка необходимых пакетов
echo "Installing software-properties-common..."
apt install software-properties-common -y

# Добавление PPA Ansible
echo "Adding Ansible PPA..."
add-apt-repository ppa:ansible/ansible -y

# Обновление списка пакетов после добавления PPA
echo "Updating package list again..."
apt update -y

# Установка Ansible
echo "Installing Ansible..."
apt install ansible -y

# Создание пользователя 'ansible'
echo "Creating user 'ansible'..."
useradd -m -s /bin/bash ansible

# Установка пароля для пользователя 'ansible'
read -sp "Enter password for user 'ansible': " ansible_password
echo
echo "Setting password for user 'ansible'..."
echo "ansible:$ansible_password" | chpasswd

# Добавление пользователя 'ansible' в группу sudo
echo "Adding user 'ansible' to sudo group..."
usermod -aG sudo ansible

echo "Ansible installation and user creation completed!"

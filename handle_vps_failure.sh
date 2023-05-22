#!/bin/bash


systemctl restart vps-service

vps-scaling-script.sh $1

echo "$(date): Ошибка VPS: $1. Выполняется обработка ошибки..." >> /var/log/vps-error.log

echo "Ошибка VPS: $1"


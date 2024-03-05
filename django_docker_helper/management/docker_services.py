services = {
    "postgres": {
        "image": "postgres:latest",
        "environment": {
            "POSTGRES_DB": "${POSTGRES_DB}",
            "POSTGRES_USER": "${POSTGRES_USER}",
            "POSTGRES_PASSWORD": "${POSTGRES_PASSWORD}",
        },
        "restart": "unless-stopped",
        "volumes": ["./data/db:/var/lib/postgresql/data"],
        "ports": ["5672:5672"],
    },
    "mysql": {
        "image": "mysql:latest",
        "environment": {
            "MYSQL_DATABASE": "${MYSQL_DATABASE}",
            "MYSQL_USER": "${MYSQL_USER}",
            "MYSQL_PASSWORD": "${MYSQL_PASSWORD}",
        },
        "restart": "unless-stopped",
        "volumes": ["./data/db:/var/lib/mysql/data"],
        "ports": ["3306:3306"],
    },
    "redis": {
        "image": "redis:latest",
        "restart": "unless-stopped",
        "volumes":["./data/redis:/data"],
        "ports": ["6379:6379"],
    },
    "rabbitmq": {
        "image": "rabbitmq:management",
        "ports": ["5672:5672", "15672:15672"],
        "volumes":["./data/rabbitmq:/data"],
        "restart": "unless-stopped",
    },
    "nginx": {
        "image": "nginx:latest",
        "restart": "unless-stopped",
        "volumes": [".:/code"],
        "ports": ["80:80"],
    }
}

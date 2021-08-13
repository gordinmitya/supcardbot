Prepare:
create file `secret.env` with ```TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE```


Development Run command: 
```docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up -d```

Production:
``````docker-compose docker-compose.yaml up -d```

Or without docker:
```export "$(cat secret.env)" && python src/main.py```

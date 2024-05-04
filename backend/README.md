# PromptSLR Backend Codebase
Run the following scripts in the current directory:

1. Create a conda environment using the following command:
```bash
conda create env -f env.yml
```

### Setup Prisma
1. Install MySQL or PostgreSQL(currently used in the project) and create a database.
2. Modfiy the connection string on line 3 in `backend/utils/schema/schema.prisma` to point to your database.
3. Run the following commands in the `backend` directory:
```bash
prisma db push --schema utils/schema/schema.prisma
```

### Run the server
1. Run the following command in the `backend` directory:
```bash
python app.py
```
> It will start the server on [http://localhost:8000](http://localhost:8000)

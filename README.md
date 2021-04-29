# Search Content

Web Application for fetching Google Custom Search API and cleaning results for online courses and articles.

## Backend (Flask)

### Installation

```bash
cd backend
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Usage

Functions included

- fetch_custom_search
- history
- engine

Use functions-framework for develop.

```bash
functions-framework --target ${FUNCTION_NAME} --debug --port ${PORT} # default 8080
```

### Deploy

```bash
gcloud beta functions deploy ${FUNCTION_NAME} --region asia-southeast2 --trigger-http --runtime python37 --project ${PROJECT_ID}
```

## Frontend (Angular)

### Installation

```bash
cd frontend
```

Install packages via npm.

```bash
npm install
```

### Usage

```bash
ng serve
```

Make sure the port in environment match with our backend.

### Deploy

Build our frontend project first.

```bash
ng build --prod
```

And then deploy to firebase hosting.

```bash
ng deploy
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

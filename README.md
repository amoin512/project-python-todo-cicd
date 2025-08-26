# Python Todo List App with GitHub Actions CI/CD to GKE

This repository contains a command-line **Todo-List application** coded in Python, along with a **GitHub Actions CI/CD pipeline** that automates:
- Building a docker image of the app.
- Pushing the image to Docker Hub.
- Testing the container locally.
- Deploying the application GKE.

## Features of the App

The app creates a text file 'todo_list.txt' to store tasks persistently which provides a simple menu-driven interface:
- **Show Task** - Displays all taks from `todo_list.txt`.
- **Add Task** - Allows user to enter:
  - Unique ID (auto-generated)
  - Task description
  - Deadline
- **Complete Task** - Removes a task by entering its ID.
- **Exit** - Closes the program.

## GitHub Actions CI/CD Workflow

The pipeline is defnied in `.gtihub/workflows/deploy.yml`. 
It runs automatically on every push to the master branch.

**Jobs:**
1. **Build & Push** - Creates a Docker image and pushes it to Docker Hub.

```
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Get code for runner
        uses: actions/checkout@v4
      - name: Build Image
        run: docker build -t todo-list-image:v3 .
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Tag and push the image
        run: |
          docker image ls
          docker tag todo-list-image:v3 moina512/python-todo-list-repo:v3
          docker push moina512/python-todo-list-repo:v3
          echo "Build and push have been successful!"
```

2. **Test** - Runs the container locally with sample input.

```
  test-on-docker:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Deoloy on Docker
        run:  echo 4 | docker run -i moina512/python-todo-list-repo:v3
```

3. **Deploy** - Authenticates to GKE, applies Kubernetes manifests, and verifies pods.

```
  login-and-deploy-to-GKE:
    needs: test-on-docker
    if: success()
    runs-on: ubuntu-latest
    steps:
      - name: Get code for runner
        uses: actions/checkout@v4
      - name: Install gcloud CLI
        uses: google-github-actions/auth@v2
        with:
          project_id: ${{ env.PROJECT_ID }}
          credentials_json: ${{ secrets.GKE_SA_KEY }}
      
      - name: Get GKE credentials
        uses: google-github-actions/get-gke-credentials@v2
        with:
          cluster_name: ${{ env.GKE_CLUSTER }}
          location: ${{ env.GKE_LOCATION }}
      
      - id: 'test-get-pods'
        run: kubectl get pods #requires Kubernetes Engine Developer role

      - name: Deploy to GKE
        run: |
          kubectl create -f resources.yml
          kubectl get pods  
```

## Accessing the App in GKE

Since this is a **CLI application**, it does not expose a web endpoint. We can **exec** into a running pod and interact with the Todo List inside the container.

1. **Exec into the pod**

```
kubectl exec -it <pod-name> -- python code.py
```

2. **Example interactive session**

```
== TODO LIST ==
[1] show task
[2] add task
[3] complete task
[4] exit
Your choice:
```
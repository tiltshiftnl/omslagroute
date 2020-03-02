#!groovy

/*
* TODO: Change 'when' conditions to 'tag "v*"', to prevent us pushing to
  production when not intended (just because we tagged something that was not a
  release)
* TODO: Tag production image with git tag as well
* TODO: DRY-up: refacter image pushing & deployment to a function
*/

pipeline {
  agent any
  environment {
    DOCKER_IMAGE = "fixxx/omslagroute"
    APP = "omslagroute"
    DOCKER_REGISTRY = "repo.secure.amsterdam.nl"
  }

  stages {
    stage("Checkout") {
      steps {
        checkout scm
        script {
          env.COMMIT_HASH = sh(returnStdout: true, script: "git log -n 1 --pretty=format:'%h'").trim()
        }
      }
    }

    stage("Build docker image") {
      // We only build a docker image when we're not deploying to production,
      // to make make sure images deployed to production are deployed to
      // acceptance first.
      //
      // To deploy to production, tag an existing commit (that has already been
      // build) and push the tag.
      when { not { buildingTag() } }

      steps {
        script {
          def image = docker.build("${env.DOCKER_REGISTRY}/${env.DOCKER_IMAGE}:${env.COMMIT_HASH}",
            "--no-cache " +
            "--build-arg COMMIT_HASH=${env.COMMIT_HASH} " +
            "--shm-size 1G " +
            " ./app")
          image.push()
          image.push("latest")
        }
      }
    }

    stage("Push acceptance image") {
      when { expression { "master" == env.BRANCH_NAME } }
      steps {
        script {
          def image = docker.image("${env.DOCKER_REGISTRY}/${env.DOCKER_IMAGE}:${env.COMMIT_HASH}")
          image.push("acceptance")
        }
      }
    }

    stage("Deploy to acceptance") {
      when { expression { "master" == env.BRANCH_NAME } }
      steps {
        build job: 'Subtask_Openstack_Playbook',
          parameters: [
              [$class: 'StringParameterValue', name: 'INVENTORY', value: 'acceptance'],
              [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy.yml'],
              [$class: 'StringParameterValue', name: 'PLAYBOOKPARAMS', value: "-e platform=secure -e app=${env.APP}"],
          ]
      }
    }

    stage("Push production image") {
      when { expression { "production" == env.BRANCH_NAME } }
      steps {
        script {
          def image = docker.image("${env.DOCKER_REGISTRY}/${env.DOCKER_IMAGE}:${env.COMMIT_HASH}")
          image.push("production")
        }
      }
    }

    stage("Deploy to production") {
      when { expression { "production" == env.BRANCH_NAME } }
      steps {
        build job: 'Subtask_Openstack_Playbook',
          parameters: [
              [$class: 'StringParameterValue', name: 'INVENTORY', value: 'production'],
              [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy.yml'],
              [$class: 'StringParameterValue', name: 'PLAYBOOKPARAMS', value: '-e platform=secure -e app=omslagroute'],
          ]
      }
    }
  }
}

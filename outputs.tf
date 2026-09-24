output "pipeline_name" {
  description = "Name of the CI/CD pipeline."
  value       = aws_codepipeline.pipeline.name
}

output "codecommit_clone_url_http" {
  description = "HTTPS clone URL of the source repository."
  value       = aws_codecommit_repository.app_repo.clone_url_http
}

output "artifacts_bucket" {
  description = "Name of the S3 bucket storing pipeline artifacts."
  value       = aws_s3_bucket.artifacts.bucket
}

output "codebuild_project_name" {
  description = "Name of the CodeBuild project that packages the application."
  value       = aws_codebuild_project.build.name
}

output "cloudformation_stack_name" {
  description = "Name of the CloudFormation stack deployed by the pipeline."
  value       = var.app_stack_name
}

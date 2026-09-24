variable "project_name" {
  description = "Project name used as prefix for all resources."
  type        = string
  default     = "floci-cicd"
}

variable "region" {
  description = "AWS region (simulated by floci)."
  type        = string
  default     = "us-east-1"
}

variable "repo_branch" {
  description = "Branch of the source repository that triggers the pipeline."
  type        = string
  default     = "main"
}

variable "app_stack_name" {
  description = "Name of the CloudFormation stack deployed by the pipeline's Deploy stage."
  type        = string
  default     = "floci-cicd-item-api"
}

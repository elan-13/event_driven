# Fetch the YAML contents
data "kubectl_file_documents" "redis" {
  content = file("../k8s/redis.yaml")
}

data "kubectl_file_documents" "ride_service" {
  content = file("../k8s/ride-service/deployment.yaml")
}

data "kubectl_file_documents" "matching_service" {
  content = file("../k8s/matching-service/deployment.yaml")
}

# Apply Redis
resource "kubectl_manifest" "redis_manifests" {
  count     = length(data.kubectl_file_documents.redis.documents)
  yaml_body = element(data.kubectl_file_documents.redis.documents, count.index)
}

# Apply Ride Service
resource "kubectl_manifest" "ride_service_manifests" {
  count     = length(data.kubectl_file_documents.ride_service.documents)
  yaml_body = element(data.kubectl_file_documents.ride_service.documents, count.index)
  depends_on = [kubectl_manifest.redis_manifests]
}

# Apply Matching Service
resource "kubectl_manifest" "matching_service_manifests" {
  count     = length(data.kubectl_file_documents.matching_service.documents)
  yaml_body = element(data.kubectl_file_documents.matching_service.documents, count.index)
  depends_on = [kubectl_manifest.redis_manifests]
}

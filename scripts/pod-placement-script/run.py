from kubernetes import client, config
import json
import sys

namespace="sre"
label="nginx"

def main():
  config.load_kube_config()
  client_core_v1_api = client.CoreV1Api()
  az_count = {}
  node_count = {}
  all_nodes = client_core_v1_api.list_node()
  pod_phase, az_count, node_count = count_pod_distribution(client_core_v1_api, all_nodes, az_count, node_count)
  replica_count = 0
  for key,value in pod_phase.items():
    replica_count = replica_count + value


  print(f"Replicas", replica_count)
  print("Pods")
  print(json.dumps(pod_phase, indent=2))
  print("AZ distribution")
  print(json.dumps(az_count, indent=2, sort_keys=True))
  print("Node distribution")
  print(json.dumps(node_count, indent=2, sort_keys=True))

def count_pod_distribution(client_core_v1_api, all_nodes, az_count, node_count):
  pod_phase = {}
  deployment_pods = client_core_v1_api.list_namespaced_pod(namespace=namespace, label_selector=label)
  for pod in deployment_pods.items:
      pod_phase[pod.status.phase] = pod_phase.get(pod.status.phase, 0) + 1
      az_count, node_count = count_nodes_zones(all_nodes, pod.spec.node_name, az_count, node_count)

  return pod_phase, az_count, node_count

def count_nodes_zones(all_nodes, node_name, az_count, node_count):

  for node in all_nodes.items:
    if node.metadata.name == node_name:
      node_count[node.metadata.name] = node_count.get(node.metadata.name, 0) + 1
      zone = node.metadata.labels['topology.kubernetes.io/zone']      
      az_count[zone] = az_count.get(zone, 0) + 1

  return az_count, node_count


if __name__ == '__main__':
    main()


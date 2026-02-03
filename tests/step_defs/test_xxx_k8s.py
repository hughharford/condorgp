# # from kubernetes import client, config

# # # Configs can be set in Configuration class directly or using helper utility
# # config.load_kube_config()

# # v1 = client.CoreV1Api()
# # print("Listing pods with their IPs:")
# # ret = v1.list_pod_for_all_namespaces(watch=False)
# # for i in ret.items:
# #     print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


# # Copyright 2016 The Kubernetes Authors.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

# """
# Reads the list of available API versions and prints them. Similar to running
# `kubectl api-versions`.
# """

# from kubernetes import client, config


# def main():
#     # Configs can be set in Configuration class directly or using helper
#     # utility. If no argument provided, the config will be loaded from
#     # default location.
#     config.load_kube_config()

#     print("Supported APIs (* is preferred version):")
#     print(f"{'core':<40} {','.join(client.CoreApi().get_api_versions().versions)}")
#     for api in client.ApisApi().get_api_versions().groups:
#         versions = []
#         for v in api.versions:
#             name = ""
#             if v.version == api.preferred_version.version and len(
#                     api.versions) > 1:
#                 name += "*"
#             name += v.version
#             versions.append(name)
#         print(f"{api.name:<40} {','.join(versions)}")


# if __name__ == '__main__':
#     main()

# Copyright 2016 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Allows you to pick a context and then lists all pods in the chosen context. A
context includes a cluster, a user, and a namespace.

Please install the pick library before running this example.
"""

from pick import pick  # install pick using `pip install pick`

from kubernetes import client, config
from kubernetes.client import configuration


def main():
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return
    contexts = [context['name'] for context in contexts]
    active_index = contexts.index(active_context['name'])
    option, _ = pick(contexts, title="Pick the context to load",
                     default_index=active_index)
    # Configs can be set in Configuration class directly or using helper
    # utility
    config.load_kube_config(context=option)

    print(f"{config.kube_config
          }")

    print(f"Active host is {configuration.Configuration().host}")

    v1 = client.CoreV1Api()
    # print("Listing pods with their IPs:")
    # ret = v1.list_pod_for_all_namespaces(watch=False)
    # for item in ret.items:
    #     print(
    #         "%s\t%s\t%s" %
    #         (item.status.pod_ip,
    #          item.metadata.namespace,
    #          item.metadata.name))

    # v1.get_api_resources_with_http_info()

    print("Looking to connect and find out something!...")
    v1.list_pod_for_all_namespaces()

if __name__ == '__main__':
    main()

import docker



# docker run -it cgp_nt_base
# python condorgp/evaluation/run_naut.py

print('running docker attempt')

# client = docker.from_env()

# container = client.containers.run(
#     image="cgp_nt_base",
#     command=["echo", "Hello World"],
#     # command=["python", "condorgp/evaluation/run_naut.py"],
#     name='new_container_1',
#     environment={'pythonunbuffered': 1},
#     detach=True,
#     )

# print(f'container = {container}')
# # print(f'container = {container.logs().strip()}')

# # for line in container.logs(stream=True): #
# #   print(line)
# #   # this prints out single letters at a time


# container.stop()
# container.remove()

from python_on_whales import docker

output_generator = docker.run(image="cgp_nt_base",
                              command=["python", "condorgp/evaluation/run_naut.py"],
                              stream=True,
                              detach=False
                              )
# container = docker.run(image="cgp_nt_base",
#                     command=["python", "condorgp/evaluation/run_naut.py"],
#                     attach_stdout=True,
#                     attach_stderr=True,
#                     detach=True)
# print(container.config)



for stream_type, stream_content in output_generator:
    print(f"Stream type: {stream_type}, stream content: {stream_content}")

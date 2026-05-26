from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="OJPob1K0te2vvBOc175w"
)

result = client.run_workflow(
    workspace_name="schumaja-katharineum-de",
    workflow_id="detect-and-classify-3",
    images={
        "image": "banana.jpg"
    },
    parameters={
        "classes": "ripe,overripe,freshripe,freshunripe,rotten,unripe"
    },
    use_cache=True
)

print(result)

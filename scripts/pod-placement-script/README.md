# Pod placement script

- Requires <https://github.com/kubernetes-client/python>

Current namespace and pod labels are defined within the script

```console
$ python3 run.py
Replicas 5
Pods
{
  "Running": 5
}
AZ distribution
{
  "us-west-2a": 2,
  "us-west-2c": 3
}
Node distribution
{
  "ip-172-19-150-124.us-west-2.compute.internal": 3,
  "ip-172-19-73-152.us-west-2.compute.internal": 2
}
```

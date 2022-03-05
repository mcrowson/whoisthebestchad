from flask import Flask, request, redirect
import boto3
import os

flask_app = Flask(__name__)


@flask_app.route("/")
def index():
    client = boto3.client("route53")
    if chosen_chad := request.args.get('chosen_chad'):
        # set the chad
        if chosen_chad not in ("kosie", "barbe"):
            return "Invalid Chad Supplied", 400

        response = client.change_resource_record_sets(
            ChangeBatch={
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": "chosen_chad.whoisthebestchad.com",
                            "ResourceRecords": [
                                {
                                    "Value": f'"{chosen_chad}"',
                                },
                            ],
                            "TTL": 300,
                            "Type": "TXT",
                        },
                    },
                ]
            },
            HostedZoneId=os.environ.get("zone_id"),
        )
        return redirect('/')
    else:
        # Get the chad
        response = client.list_resource_record_sets(
            StartRecordType="TXT",
            StartRecordName="chosen_chad.whoisthebestchad.com",
            HostedZoneId=os.environ.get("zone_id"),
            MaxItems="1",
        )

        chosen_chad = response["ResourceRecordSets"][0]["ResourceRecords"][0][
            "Value"
        ].replace('"', "")

        chad_imgs = {
            "kosie": "https://s3.amazonaws.com/static.whoisthebestchad.com/dog1.jpg",
            "barbe": "https://s3.amazonaws.com/static.whoisthebestchad.com/dog2.jpg",
        }

        img = chad_imgs.get(chosen_chad)
        return f"""
            <html><body><img src="{img}"/></body></html>
        """

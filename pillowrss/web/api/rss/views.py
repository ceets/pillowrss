import json
import requests
from fastapi import APIRouter, HTTPException, Response
import datetime
router = APIRouter()


@router.get("/{community_name}/atom.xml", response_model=str)
async def get_rss(
    community_name: str,
) :
    """
    RSS-ify community on Pillowfort with Atom format

    :param community_name: Pillowfort community.
    :returns: atom.xml file.
    """

    res = requests.get(
        f"https://www.pillowfort.social/community/{community_name}/posts/json"
    )

    if res.status_code < 200 or res.status_code >= 300:
        raise HTTPException(status_code=404, detail="Item not found")

    response = json.loads(res.text)

    def serialize_entry(
        title, content, username, url, publish_date, update_date
    ) -> str:
        return f"""
        <entry>
        <updated>{update_date}</updated>
        <author><name>{username}</name></author>
        <content>
            <![CDATA[{content}]]>
        </content>
        <id>{url}</id>
        <link href="{url}"/>
        <published>{publish_date}</published>
        <summary>
            <![CDATA[{content[:5000]}]]>
        </summary>
        <title>{title}</title>
        </entry>"""

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>"""
    entries = ""
    for item in response:
        title = item["title"] if item["title"] else ""
        entries += serialize_entry(
            title,
            item["content"],
            item["username"],
            "https://pillowfort.social/" + "posts" + "/" + str(item["id"]),
            item["publish_at"],
            item["updated_at"],
        )
    feed = f"""<feed  xmlns="http://www.w3.org/2005/Atom"><updated>{datetime.datetime.now(datetime.timezone.utc).isoformat()}</updated>
        <author><name>Pillowfort</name></author>
        <id>https://pillowrss.ceets.vip/</id>
        <link href="https://pillowrss.ceets.vip/api/{community_name}/atom.xml" rel="self"/>
        <rights>All rights reserved 2026, Pillowfort LLC</rights>
        <subtitle><![CDATA[<a href="https://pillowfort.social/donations">Help Pillowfort keep the lights on</a>]]></subtitle>
        <title>Pillowfort feed - '{community_name}'</title>
        {entries}
        </feed>"""
    xml_content += feed
    return Response(content=xml_content, media_type="application/xml")

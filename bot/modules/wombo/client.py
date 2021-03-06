import logging
from copy import copy
from typing import List, Optional

import httpx

from bot.core.config import api_key
from bot.core.exceptions import WomboAPIException

logger = logging.getLogger(__name__)

WOMBO_API_URL = "https://api.luan.tools/api"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"bearer {api_key}",
}


class WomboAPIClient:
    def __init__(self) -> None:
        self.session = httpx.AsyncClient(verify=False)

    async def start_dream(self, *, use_target_image: bool = False) -> None:
        body = {"use_target_image": use_target_image}
        logger.debug(
            f"Sending initial POST request to create task | Data: {str(body)} | Headers: {str(HEADERS)}"
        )
        r = await self.session.post(
            WOMBO_API_URL + "/tasks/", json=body, headers=HEADERS
        )
        logger.debug(
            f"Received response from Wombo API | Status: {r.status_code} | Response: {r.text}"
        )
        if r.status_code != 200:
            raise WomboAPIException

        j = r.json()
        self.dream_id = j["id"]
        self.target_image_info = j["target_image_url"]
        logger.debug(
            f"Saved dream ID ({self.dream_id}) and target image info ({str(self.target_image_info)})"
        )

    # This is only required to be called if the 'use_target_image' parameter was set to True in the 'start_dream_task' function
    async def post_target_image(self, image_bytes: bytes) -> None:
        data = self.target_image_info
        init_data = copy(data)
        data["file"] = image_bytes
        logger.debug(
            f"Sending POST request to upload target image | Data (minus image): {init_data} | Image Size: {len(image_bytes)}"
        )
        r = await self.session.post(data["url"], data=data)
        logger.debug(
            f"Received response from Wombo API | Status: {r.status_code} | Response: {r.text}"
        )
        if r.status_code != 200:
            raise WomboAPIException

    async def put_dream_data(
        self,
        *,
        prompt: str,
        style: int,
        height: int,
        width: int,
        target_image_weight: float,
    ):
        body = {
            "input_spec": {
                "prompt": prompt,
                "style": style,
                "height": height,
                "width": width,
                "target_image_weight": target_image_weight,
            }
        }
        logger.debug(f"Sending PUT request to update dream data | Data: {str(body)}")
        r = await self.session.put(
            WOMBO_API_URL + "/tasks/" + self.dream_id, json=body, headers=HEADERS
        )
        logger.debug(
            f"Received response from Wombo API | Status: {r.status_code} | Response: {r.text}"
        )
        if r.status_code != 200:
            raise WomboAPIException

    # You will most likely need to call this function multiple times
    async def get_dream_data(self) -> Optional[dict]:
        logger.debug(f"Sending GET request to get dream data")
        r = await self.session.get(
            WOMBO_API_URL + "/tasks/" + self.dream_id, headers=HEADERS
        )
        logger.debug(
            f"Received response from Wombo API | Status: {r.status_code} | Response: {r.text}"
        )
        if r.status_code != 200:
            raise WomboAPIException

        j = r.json()
        if j["state"] == "failed":
            raise WomboAPIException
        elif j["state"] == "completed":
            await self.session.aclose()
            return j

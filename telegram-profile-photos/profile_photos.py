from typing import List
import requests
from pydantic import BaseModel

TELEGRAM_BOT_TOKEN = '{TOKEN}'

class PhotoSize(BaseModel):
    """
    This object represents one size of a photo or a file / sticker thumbnail.

    Attributes:
        file_id (:obj:`str`): Unique identifier for this file.
        file_unique_id (:obj:`str`): Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        width (:obj:`int`): Photo width.
        height (:obj:`int`): Photo height.
        file_size (:obj:`int`): Optional. File size.
    """
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int

class TelegramProfilePhotos(BaseModel):
    """
    This object represent a user's profile pictures.

    Attributes:
        total_count (:obj:`int`): Total number of profile pictures the target user has.
        photos (List[List[:class:`PhotoSize`]]): Requested profile pictures (in up to 4 sizes each).
    """
    total_count: int
    photos: List[List[PhotoSize]]

def get_profile_photos(user_id: str) -> TelegramProfilePhotos:
    """
    Get a user's profile pictures.

    Args:
        user_id (:obj:`str`): User identifier.

    Returns:
        :class:`TelegramProfilePhotos`: Requested profile pictures.
    """
    response = requests.get(
        f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUserProfilePhotos?user_id={user_id}',
        timeout=1)

    if response.status_code != 200:
        return None

    body = response.json()

    return TelegramProfilePhotos(**body['result'])

def get_file(file_id: str) -> bytes:
    """
    Get a file.

    Args:
        file_id (:obj:`str`): File identifier.

    Returns:
        :obj:`bytes`: File content.
    """
    response = requests.get(
        f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}',
        timeout=1)

    if response.status_code != 200:
        return None

    body = response.json()

    file_path = body['result']['file_path']

    response = requests.get(
        f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}',
        timeout=1)

    if response.status_code != 200:
        return None

    return response.content

def main():
    """
    Main function.
    """
    user_id = '412695732'
    profile_photos = get_profile_photos(user_id)

    if profile_photos is None:
        print('Failed to get profile photos')
        return

    # Download profile photos
    for i, photos in enumerate(profile_photos.photos):
        for j, photo in enumerate(photos):
            file = get_file(photo.file_id)
            with open(f'photo_{i}_{j}.jpg', 'wb') as f:
                f.write(file)

    # Or send a one to your front-end in Bytearray format
    first_photo = profile_photos.photos[0][0].file_id
    first_photo_file = get_file(first_photo)
    byte_array = bytearray(first_photo_file)

if __name__ == '__main__':
    main()

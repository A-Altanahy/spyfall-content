# Spyfall Game Content

This repository hosts the dynamic content (images and categories) for the Spyfall game.

## How to Add Content

1.  **Add Images**: Upload your image files to the `images/` folder.
2.  **Update Manifest**: Edit `data.json` to include the new images.

### `data.json` Structure

```json
{
  "version": 1,
  "categories": [
    {
      "id": 1,            // Unique ID for the category
      "name": "Category Name",
      "enabled": true,
      "images": [
        {
          "name": "Image Name",
          "file": "images/filename.jpg"  // Path relative to repo root
        }
      ]
    }
  ]
}
```

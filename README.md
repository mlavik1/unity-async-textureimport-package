# Unity Async Texture Importer (automatic builds)

This repository is simply a set of build scripts and actions for building and packaging unity-async-textureimport for Unity.
See main repo here: https://codeberg.org/matiaslavik/unity-async-textureimport

This is a faster alternative to [Texture2D.LoadImage](https://docs.unity3d.com/530/Documentation/ScriptReference/Texture2D.LoadImage.html) and , which can only be used on the main thread - and which will block the thread until it's done.

# How to use
Create a [coroutine](https://docs.unity3d.com/Manual/Coroutines.html), and from there do this:
```csharp
TextureImporter importer = new TextureImporter();
yield return importer.ImportTexture(texPath, FREE_IMAGE_FORMAT.FIF_JPEG);
Texture2D tex = importer.texture;
```
See the sample scene for an example.

# What it does
The TextureImporter class has a public IEnumerator ("ImportTexture") that you can call/yield from a coroutine. It runs a task in a separate thread that loads the texture file, converts it to raw data and generates mipmaps. When the task is done, the IEnumerator will finally upload the raw data by calling [Texture2D.LoadRawTextureData](https://docs.unity3d.com/ScriptReference/Texture2D.LoadRawTextureData.html).
Since the file reading, decompressing and mipmap generation is done in a separate thread, you will be able to load large textures without causing FPS lags/hiccups.
I used [FreeImage](https://freeimage.sourceforge.io/) for the texture loading/conversion.

# License
 MIT License
 (See the "LICENSE" file)

 Note: This project uses the FreeImage library. To use this project, you should include a copy of the FreeImage license (GPL or FIPL). See more info here: https://freeimage.sourceforge.io/license.html

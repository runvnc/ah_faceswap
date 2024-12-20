from facefusionlib import swapper
from facefusionlib.swapper import DeviceProvider
from os import listdir, path
import shutil
import nanoid
from lib.providers.services import service

@service()
async def swap_face(input_ref_dir, target_image_path, context=None, skip_nsfw=False, wrap_html=False):
    """Swap faces in target image using reference faces.
    
    Args:
        input_ref_dir (str): Directory containing reference face images
        target_image_path (str): Path to target image where faces will be swapped
        context (object, optional): Service context. Defaults to None.
        skip_nsfw (bool, optional): Skip NSFW content detection. Defaults to False.
        wrap_html (bool, optional): Wrap result in HTML img tag. Defaults to False.
    
    Returns:
        str: Path to resulting image, or HTML img tag if wrap_html=True
    
    Example:
        result = await swap_face(
            "imgs/faceref/person1", 
            "imgs/target.png", 
            skip_nsfw=True,
            wrap_html=True
        )
    """
    print("-------------------- face_swap")
    # Get all files from reference directory
    input_image_paths = [path.join(input_ref_dir, f) 
                        for f in listdir(input_ref_dir) 
                        if path.isfile(path.join(input_ref_dir, f))]
    
    print("input_ref_dir:", input_ref_dir)
    print("input_image_paths:", input_image_paths)
    print("target_image_path:", target_image_path)
    
    try:
        # Perform face swap operation
        result = swapper.swap_face(
            source_paths=input_image_paths,
            target_path=target_image_path,
            provider=DeviceProvider.GPU,
            detector_score=0.65,
            mask_blur=0.6,
            skip_nsfw=skip_nsfw,
            landmarker_score=0.005
        )
        print("face swap result image: ", result)
        
        # Generate unique filename and save result
        new_fname = path.join("imgs", f"{nanoid.generate()}.png")
        result = shutil.copy(result, new_fname)

        # Optionally wrap result in HTML img tag
        if wrap_html:
            result = f'<img src="{result}" style="max-width: 100%; height: auto;" />'
            
        return result
        
    except Exception as e:
        print(f"Error in face_swap: {str(e)}")
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(swap_face("imgs/faceref/g", "imgs/target.png", skip_nsfw=True))

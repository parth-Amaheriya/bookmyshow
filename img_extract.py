from DrissionPage import ChromiumPage, ChromiumOptions
import base64
import os


def main():
    co = ChromiumOptions()
    co.headless(False)  
    
    page = ChromiumPage(co)
    page.get('https://in.bookmyshow.com/movies/ahd/seat-layout/ET00411383/PPAM/31875/20260427')
    page.ele("css: button[aria-label='Select Seats']",timeout=5).click()


    script = """
    let canvases = document.querySelectorAll("canvas");
    let canvasData = [];
    canvases.forEach((canvas, index) => {
        canvasData.push({ index: index, data: canvas.toDataURL() });
    });
    return canvasData;
    """
    canvas_data = page.run_js(script)

    os.makedirs('canvas_images', exist_ok=True)

    for canvas in canvas_data:
        base64_image = canvas['data'].split(",")[1] 
        img_path = f"canvas_images/canvas_image_{canvas['index'] + 1}.png"  
        with open(img_path, "wb") as img_file:
            img_file.write(base64.b64decode(base64_image))
        print(f"Saved: {img_path}")

    page.close()

if __name__ == "__main__":
    main()
from pathlib import Path

from caption_tagfile.tag_manager import TagfileManager


def test_read_write(
        tmpdir,
):
    mgr = TagfileManager()
    img = "test.jpg"
    Path(img).touch()  # Fake image
    tagfile = mgr.create(img, captions={"test": "hello"}, tags=["tag1"], )
    loaded = mgr.read(img)
    assert loaded.captions["test"] == "hello"
    assert loaded.hash is not None


def test_read_write2(
        tmpdir,
):
    test_img: Path = Path(__file__).parent / "assets/images/Gustav-Klimt_the-kiss.jpg"

    # Create a new tagfile
    mgr = TagfileManager()
    tagfile = mgr.create(
        test_img,
        captions={"florence": "A painting...", "blip2": "the kiss..."},
        tags=["golden", "Klimt"],
    )

    # Read it back
    loaded = mgr.read(test_img)
    print(loaded.captions["florence"])  # "A painting..."

    # Update and write
    loaded.tags.append("art nouveau")
    mgr.write(test_img, loaded)


def test_oteretst():
    mgr = TagfileManager()

    test_img: Path = Path(__file__).parent / "assets/images/Gustav-Klimt_the-kiss.jpg"

    with open(test_img.with_suffix(test_img.suffix + ".txt"), "w") as f:
        f.write("the kiss by gustav klimt")

    # Read migrates .txt to .json
    tagfile = mgr.read(test_img)
    print(tagfile.captions)  # {'default': 'the kiss by gustav klimt'}

    # Add a new caption
    tagfile.captions["florence"] = "A painting..."
    mgr.write(test_img, tagfile)
    # .json now has both "default" and "florence"

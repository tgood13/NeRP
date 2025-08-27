import re
import pathlib
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('macosx')


def get_image_paths(root="outputs/ct_recon"):
    d = pathlib.Path(root)
    first_level = next(p for p in d.iterdir() if p.is_dir())
    second_level = next(p for p in first_level.iterdir() if p.is_dir())
    images_dir = second_level / "images"
    return sorted(images_dir.glob("*.png"))


def get_iteration_number(name: str):
    m = re.match(r"recon_(\d+)_([0-9.]+)dB\.(png)$", name)
    if not m:
        raise ValueError("Failed to locate iteration in file name")
    return int(m.group(1))


def plot_recons():

    paths = get_image_paths()

    recons = []
    ground_truth = None
    for p in paths:
        name = p.name.lower()
        if name == "train.png":
            continue
        if name == "test.png":
            ground_truth = p
            continue
        if name.startswith("recon_"):
            it = get_iteration_number(p.name)
            recons.append((it, p))

    # Sort by iteration
    recons = sorted(recons, key=lambda x: x[0])

    images_to_plot = [r[1] for r in recons]
    titles = [f"Iter {r[0]}" for r in recons]

    # Include ground truth image at the end
    if ground_truth is not None:
        images_to_plot.append(ground_truth)
        titles.append("Ground truth")

    n = len(images_to_plot)
    plt.figure(figsize=(12, 3))
    for i, (p, title) in enumerate(zip(images_to_plot, titles), start=1):
        img = Image.open(p)
        plt.subplot(1, n, i)
        plt.imshow(img, cmap="gray")
        plt.title(title, fontsize=9)
        plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_recons()

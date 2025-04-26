from api.mediafire import MediaFireAPI

if __name__ == "__main__":
    mf = MediaFireAPI(sleep_per_download=2)

    url = "https://www.mediafire.com/file/bndm1zl8b5ho6zs/Coser%2540%25E9%259B%25AA%25E6%2599%25B4Astra_%2528%25E9%259B%25AA%25E6%2599%25B4%25E5%2598%259F%25E5%2598%259F%2529_Vol.043.rar"
    folder_key = url.split("folder/")[-1].split("/")[0]

    mf.download_folder(folder_key, "output")

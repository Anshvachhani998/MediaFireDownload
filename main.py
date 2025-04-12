from api.mediafire import MediaFireAPI

if __name__ == "__main__":
    mf = MediaFireAPI(sleep_per_download=2)

    url = ""
    folder_key = url.split("folder/")[-1].split("/")[0]

    mf.download_folder(folder_key, "output")

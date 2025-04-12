# # Universities data
# with open("universities.json", encoding="utf8") as f:
#     universities = json.load(f)

# Dynamics
# URL and headers


# def create_affiliations():
#     url = "https://bircpc.ir/jury/affiliations/add"

#     for uni_fa_name, university in universities.items():
#         if university["id"]:
#             continue

#         # Prepare form data
#         files = {
#             "team_affiliation[icpcid]": (None, ""),
#             "team_affiliation[shortname]": (None, university["shortname"]),
#             "team_affiliation[name]": (None, university["name"]),
#             "team_affiliation[country]": (None, university["country"]),
#             "team_affiliation[internalcomments]": (None, ""),
#             "team_affiliation[logoFile]": ("", "", "application/octet-stream"),
#             "team_affiliation[save]": (None, ""),
#         }

#         boundary = "----WebKitFormBoundary" + "".join(
#             random.sample(string.ascii_letters + string.digits, 16)
#         )
#         m = MultipartEncoder(fields=files, boundary=boundary)
#         headers["Content-Type"] = m.content_type

#         # Make POST request
#         response = requests.post(
#             url, headers=headers, cookies=cookies, data=m, allow_redirects=False
#         )

#         # Check for redirect
#         if response.status_code in [301, 302] and "Location" in response.headers:
#             redirect_url = urljoin(url, response.headers["Location"])
#             universities[uni_fa_name]["id"] = redirect_url.split("/")[-1]
#             print(
#                 f"Redirect URL for {university['name']}: {universities[uni_fa_name]["id"]}"
#             )
#         else:
#             print(
#                 f"Failed to create affiliation for {university['name']}: {response.status_code}"
#             )

#     with open("universities.json", "w", encoding="utf8") as f:
#         json.dump(universities, f)

        avatar_match = re.search(r'"avatar":{"thumbnails":\[{"url":"(.*?)"', text)
        avatar = avatar_match.group(1) if avatar_match else ""
        
        name_match = re.search(r'"channelMetadataRenderer":{"title":"(.*?)"', text)
        name = (1) if name_match else f"@{channel}"
        
        return jsonify({
            "status": "success",
            "data": {
                "name": name,
                "handle": f"@{channel}",
                "avatar": avatar,
                "subscribers": subs,
                "views": views,
                "videos": []
            }
        })
        
    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "Request to YouTube timed out"}), 504
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

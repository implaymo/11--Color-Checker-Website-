      
      stored_image_id = 1
      image = db.get_or_404(ImageStore, stored_image_id)
      print(image)
      db.session.delete(image)
      db.session.commit()
      
      new_image = ImageStore(img_url=file)
      db.session.add(new_image)
      db.session.commit()
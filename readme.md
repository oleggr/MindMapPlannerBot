MindMapPlannerBot
---
Bot for tracking plans in mind map format

ToDo:
1. Fix long leaves names. 
    
    Currently it fails when we try to build callback data because of the length.
    - It's possible if replace callback data to callback name and transfer in it only stage id. 
    - Or not transferring leaf name in callback_data and get it by id from DB.
    ```bash
    ValueError: Resulted callback data is too long! len('cmd:view:2:10 подтягиваний за подход:default:1'.encode()) > 64
    ```
2. Add image generation for each leaf.
    - Searh for different user cases.
    - Implement image generator.
    - Reuse images to not overuse cpu and to not load lots of same images to telegram.

3. Support targets handling (add, edit actions), track them and send notifications.
4. Add notification setting to settings menu.
5. Cover happy path with tests.
6. Pack bot to docker, use postgress instead of sqllite

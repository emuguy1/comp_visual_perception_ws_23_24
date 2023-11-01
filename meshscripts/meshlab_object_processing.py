import pymeshlab
ms = pymeshlab.MeshSet()

ms.load_new_mesh("D:\Google Drive\Studium\Computational Visual Perception -\project-tests\0002e50309b44e409c96f440202d90b3.obj")
ms.compute_matrix_from_scaling_or_normalization(unitflag= True)
ms.save_current_mesh("D:\Google Drive\Studium\Computational Visual Perception -\project\objectfiles\1.obj", save_textures= False, texture_quality= -1)
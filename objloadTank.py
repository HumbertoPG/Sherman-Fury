import os
from OpenGL.GL import *
from PIL import Image

class OBJ:
    def __init__(self, filename, swapyz=False):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.materials = {}

        material = None

        try:
            with open(filename, "r") as f:
                for line in f:
                    if line.startswith('#'):
                        continue
                    values = line.split()
                    if not values:
                        continue
                    if values[0] == 'v':
                        v = list(map(float, values[1:4]))
                        if swapyz:
                            v = v[0], v[2], v[1]
                        self.vertices.append(v)
                    elif values[0] == 'vn':
                        v = list(map(float, values[1:4]))
                        if swapyz:
                            v = v[0], v[2], v[1]
                        self.normals.append(v)
                    elif values[0] == 'vt':
                        self.texcoords.append(list(map(float, values[1:3])))
                    elif values[0] == 'f':
                        face = []
                        texcoords = []
                        norms = []
                        for v in values[1:]:
                            w = v.split('/')
                            face.append(int(w[0]))
                            if len(w) >= 2 and w[1]:
                                texcoords.append(int(w[1]))
                            else:
                                texcoords.append(0)
                            if len(w) >= 3 and w[2]:
                                norms.append(int(w[2]))
                            else:
                                norms.append(0)
                        self.faces.append((face, texcoords, norms, material))
                    elif values[0] == 'usemtl':
                        material = values[1]
                    elif values[0] == 'mtllib':
                        self.load_materials(os.path.join(os.path.dirname(filename), values[1]))

            print(f"OBJ file {filename} loaded successfully.")
        except Exception as e:
            print(f"Error loading OBJ file {filename}: {e}")

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, texcoords, norms, material = face
            if material and material in self.materials:
                mtl = self.materials[material]
                if 'texture_Kd' in mtl:
                    glEnable(GL_TEXTURE_2D)
                    glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
                else:
                    glDisable(GL_TEXTURE_2D)

                # Set material properties
                if 'Kd' in mtl:
                    glColor3fv(mtl['Kd'])
                else:
                    glColor3f(1.0, 1.0, 1.0)  # Default to white color

                if 'Ka' in mtl:
                    glMaterialfv(GL_FRONT, GL_AMBIENT, mtl['Ka'])
                if 'Kd' in mtl:
                    glMaterialfv(GL_FRONT, GL_DIFFUSE, mtl['Kd'])
                if 'Ks' in mtl:
                    glMaterialfv(GL_FRONT, GL_SPECULAR, mtl['Ks'])
                if 'Ns' in mtl:
                    glMaterialfv(GL_FRONT, GL_SHININESS, mtl['Ns'])
            else:
                glColor3f(1.0, 1.0, 1.0)  # Default to white color

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if norms[i] > 0:
                    glNormal3fv(self.normals[norms[i] - 1])
                if texcoords[i] > 0:
                    glTexCoord2fv(self.texcoords[texcoords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glEndList()

    def load_materials(self, filename):
        current_dir = os.path.dirname(filename)
        mtl = None
        materials = {}
        try:
            with open(filename, "r") as f:
                for line in f:
                    if line.startswith('#'):
                        continue
                    values = line.split()
                    if not values:
                        continue
                    if values[0] == 'newmtl':
                        mtl = materials[values[1]] = {}
                    elif mtl is None:
                        continue
                    elif values[0] == 'map_Kd':
                        image_filename = values[1]
                        image_path = os.path.join(current_dir, image_filename)
                        try:
                            image = Image.open(image_path)
                            image = image.transpose(Image.FLIP_TOP_BOTTOM)
                            ix, iy, image = image.size[0], image.size[1], image.tobytes()
                            texid = glGenTextures(1)
                            glBindTexture(GL_TEXTURE_2D, texid)
                            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
                            mtl['texture_Kd'] = texid
                        except Exception as e:
                            print(f"Failed to load texture {image_path}: {e}")
                    elif values[0] == 'Kd':
                        mtl['Kd'] = list(map(float, values[1:4]))
                    elif values[0] == 'Ka':
                        mtl['Ka'] = list(map(float, values[1:4]))
                    elif values[0] == 'Ks':
                        mtl['Ks'] = list(map(float, values[1:4]))
                    elif values[0] == 'Ns':
                        mtl['Ns'] = float(values[1])
            self.materials.update(materials)
            print(f"Materials file {filename} loaded successfully.")
        except Exception as e:
            print(f"Error loading materials file {filename}: {e}")

    def render(self):
        glCallList(self.gl_list)

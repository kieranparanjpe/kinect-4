import numpy as np
import pygltflib

from src.RigData import RigData


def create_gltf_animation(data:RigData):
    gltf = pygltflib.GLTF2()
    joints = data.joints
    # Create nodes for joints
    for joint in joints:
        node = pygltflib.Node(name=joint.name)
        gltf.nodes.append(node)

    # Create animation
    animation = pygltflib.Animation()

    # Create translation channels for each joint
    for i, joint in enumerate(joints):
        # Prepare channel for this joint's translations
        sampler = pygltflib.AnimationSampler(
            input=list(range(len(position_arrays[0]))),  # frame times
            output=position_arrays[i].flatten().tolist()  # flattened positions
        )

        # Create channel mapping to node
        channel = pygltflib.AnimationChannel(
            sampler=len(gltf.animations[0].samplers) if gltf.animations else 0,
            target=pygltflib.AnimationChannelTarget(
                node=i,  # node index
                path='translation'
            )
        )

        animation.samplers.append(sampler)
        animation.channels.append(channel)

    gltf.animations.append(animation)

    # Create scene
    gltf.scenes.append(pygltflib.Scene(nodes=list(range(len(joints)))))
    gltf.scene = 0

    return gltf


# Example usage
def main():
    # Usage example
    data = RigData()
    root = RigData.Joint("Root", data)
    root.add_keyframe(0, 0, 0)
    hip = RigData.Joint("Hip", data)
    hip.add_keyframe(0, 1, 0)
    root.children.append(hip)

    gltf = create_gltf_animation(data)
    gltf.save("animated_rig.gltf")



def export_rig_to_gltf(rig_data, output_path):
    gltf = pygltflib.GLTF2()

    def traverse_joints(joint, parent_index=None):
        # Create node for this joint
        node = pygltflib.Node(
            name=joint.name,
            translation=list(joint.keyframes[0])
        )
        gltf.nodes.append(node)
        current_index = len(gltf.nodes) - 1

        # Link to parent if exists
        if parent_index is not None:
            gltf.nodes[current_index].children = [parent_index]

        # Recursively add children
        for child in joint.children:
            traverse_joints(child, current_index)

    # Start traversal from root
    traverse_joints(rig_data.joints[0])

    gltf.scenes.append(pygltflib.Scene(nodes=[0]))
    gltf.scene = 0

    gltf.save(output_path)


#export_rig_to_gltf(data, "exports/character_rig.gltf")
main()
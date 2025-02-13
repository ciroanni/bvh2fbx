import bpy
import sys
from mathutils import Vector

# Get command line arguments
print(sys.argv)
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "—"
bvh_in = argv[0]
fbx_out = argv[0].replace(".bvh", "") + ".fbx"

# Import the BVH file
# See https://docs.blender.org/api/current/bpy.ops.import_anim.html?highlight=import_anim#module-bpy.ops.import_anim
bpy.ops.import_anim.bvh(filepath=bvh_in, filter_glob="*.bvh", global_scale=1, frame_start=1, target='ARMATURE',
                        use_fps_scale=False, use_cyclic=False, rotate_mode='NATIVE', axis_forward='Z', axis_up='Y')

# add hand bones to the armature, they must be children of the lower arm bones
bpy.ops.object.mode_set(mode='EDIT')
armature = bpy.context.object.data
# get the bones
bones = armature.edit_bones
# get the lower arm bones
l_lower_arm = bones['LeftLowerArm']
r_lower_arm = bones['RightLowerArm']
# add the hand bones
l_hand = bones.new('LeftHand')
l_hand.head = l_lower_arm.tail
l_hand.tail = l_lower_arm.tail + (l_lower_arm.tail - l_lower_arm.head).normalized() * 0.1
l_hand.parent = l_lower_arm
l_hand.use_connect = False

r_hand = bones.new('RightHand')
r_hand.head = r_lower_arm.tail
r_hand.tail = r_lower_arm.tail + (r_lower_arm.tail - r_lower_arm.head).normalized() * 0.1
r_hand.parent = r_lower_arm
r_hand.use_connect = False
bpy.ops.object.mode_set(mode='OBJECT')


# Export as FBX
# See https://docs.blender.org/api/current/bpy.ops.export_scene.html
bpy.ops.export_scene.fbx(filepath=fbx_out, axis_forward='Z',
                         axis_up='Y', use_selection=True, apply_scale_options='FBX_SCALE_NONE')

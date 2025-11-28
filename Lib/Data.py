#____Obj____
class keypoint:
	x = 0
	y = 0
	z = 0

	vis = 0

#____wrappers____
def get_Joint_Map(name, Json_lib):
	return Json_lib.File.load(f'Content/Joint-Maps/{name}.json')
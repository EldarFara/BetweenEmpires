
uniform float4x4 matWorldViewProj;
#ifndef DISABLE_GPU_SKINNING
uniform float4x4 matWorldArray[NUM_WORLD_MATRICES];
#endif

#ifndef DISABLE_GPU_SKINNING
vec4 skinning_deform(vec4 vPosition, vec4 vBlendWeights, vec4 vBlendIndices)
{
	return 	  mul(matWorldArray[int(vBlendIndices.x)], vPosition) * vBlendWeights.x
			+ mul(matWorldArray[int(vBlendIndices.y)], vPosition) * vBlendWeights.y
			+ mul(matWorldArray[int(vBlendIndices.z)], vPosition) * vBlendWeights.z
			+ mul(matWorldArray[int(vBlendIndices.w)], vPosition) * vBlendWeights.w;
}
#endif

float get_depth(float4 pos)
{	
	float real_z = (pos.z * 0.5) + 0.5;
	#ifdef VIEW_SPACE
		return real_z;
	#else
		return real_z / far_clip;	//STR_TODO: use inv_far_clip & mul 
	#endif
}


attribute vec3 inPosition;
attribute vec2 inTexCoord;

varying float2 Tex0;
varying float3 LightDir;
varying float4 LightDif;
varying float3 CameraDir;
varying float4 PosWater;
varying float Fog;

float get_wave_height_temp(vec2 pos, float coef, float freq1, float freq2, float time)
{
	return coef * sin( (pos.x + pos.y) * freq1 + time) * cos((pos.x - pos.y) * freq2 + (time + 4.0));// + (coef * 0.05 * sin( (pos[0]*pos[1]) * (freq1 * 200 * time) + time));
}

void main()
{
	float4 vWorldPos = mul(matWorld, vec4(inPosition, 1.0));
	
	float3 viewVec = vCameraPos.xyz - vWorldPos.xyz;
	float wave_distance_factor = (1.0 - saturate(length(viewVec) * 0.01));	//no wave after 100 meters
	
	vWorldPos.z += get_wave_height_temp(vWorldPos.xy, debug_vector.z, debug_vector.x, debug_vector.y, time_var) * wave_distance_factor; 

	gl_Position = mul(matViewProj, vWorldPos);
	PosWater = mul(matWaterViewProj, vWorldPos);

	//calculate new normal:
	float3 vNormal;
	if(wave_distance_factor > 0.0)
	{
		float3 near_wave_heights[2];
		near_wave_heights[0].xy = vWorldPos.xy + float2(0.1, 0.0);
		near_wave_heights[1].xy = vWorldPos.xy + float2(0.0, 1.0);
		
		near_wave_heights[0].z = get_wave_height_temp(near_wave_heights[0].xy, debug_vector.z, debug_vector.x, debug_vector.y, time_var);
		near_wave_heights[1].z = get_wave_height_temp(near_wave_heights[1].xy, debug_vector.z, debug_vector.x, debug_vector.y, time_var);
		
		float3 v0 = normalize(near_wave_heights[0] - vWorldPos.xyz);
		float3 v1 = normalize(near_wave_heights[1] - vWorldPos.xyz);
		
		vNormal = cross(v0, v1);
	}
	else 
	{
		vNormal = float3(0.0, 0.0, 1.0);
	}
		
	float3 vWorldN = vNormal;
	float3 vWorld_tangent  = float3(1.0, 0.0, 0.0);
	float3 vWorld_binormal = normalize(cross(vWorld_tangent, vNormal));

	float3x3 TBNMatrix = float3x3_transpose(vWorld_tangent, vWorld_binormal, vWorldN); 

	float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos.xyz);
	CameraDir = mul(TBNMatrix, point_to_camera_normal);

	Tex0 = vWorldPos.xy;

	LightDir = vec3(0.0);
	LightDif = vAmbientColor;

	//directional lights, compute diffuse color
	LightDir += mul(TBNMatrix, -vSunDir.xyz);
	LightDif += vSunColor;
	LightDir = normalize(LightDir);

	//apply fog
	float3 P = mul(matWorldView, vec4(inPosition, 1.0)).xyz; //position attribute view space
	float d = length(P);
	Fog = get_fog_amount_new(d, vWorldPos.z);
}
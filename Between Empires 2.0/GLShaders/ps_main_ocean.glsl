
varying float4 Pos;
varying float2 Tex0;
varying float3 LightDir;
varying float4 LightDif;
varying float3 CameraDir;
varying float4 PosWater;
varying float Fog;

void main()
{	
	const float texture2D_factor = 1.0;
	
	float3 normal;
	normal.xy = (2.0 * texture2D(NormalTextureSampler, Tex0 * texture2D_factor).ag - 1.0);
	normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));
	
	const float detail_factor = 16.0 * texture2D_factor;
	float3 detail_normal;
	detail_normal.xy = (2.0 * texture2D(NormalTextureSampler, Tex0 * detail_factor).ag - 1.0);
	detail_normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));
	
	float NdotL = saturate(dot(normal, LightDir));
	
	float4 tex = texture2D(ReflectionTextureSampler, 0.5 * normal.xy + float2(0.5 + 0.5 * (PosWater.x / PosWater.w), 0.5 - 0.5 * (PosWater.y / PosWater.w)));
	INPUT_OUTPUT_GAMMA(tex.rgb);
	
	vec4 finalColor = 0.01 * NdotL * LightDif;
	
	float3 vView = normalize(CameraDir);

	// Fresnel term
	float fresnel = 1.0 - (saturate(dot(vView, normal)));
	fresnel = 0.0204 + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);

	finalColor.rgb += (tex.rgb * fresnel);
	finalColor.a = 1.0 - 0.3 * CameraDir.z;
	
	float3 cWaterColor = 2.0 * float3(20.0 / 255.0, 45.0 / 255.0, 100.0 / 255.0) * vSunColor.rgb;
	
	float fog_fresnel_factor = saturate(dot(CameraDir, normal));
	fog_fresnel_factor *= fog_fresnel_factor;
	fog_fresnel_factor *= fog_fresnel_factor;
	finalColor.rgb += cWaterColor * fog_fresnel_factor;
	
	OUTPUT_GAMMA(finalColor.rgb);
	finalColor.a = 1.0;

	gl_FragColor = finalColor;
}



attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;

varying vec3 outNormal;
varying vec4 outColor0;
varying vec4 outColor1;
varying vec2 outTexCoord;
varying float outFog;

void main()
{
	gl_Position = mul(matWorldViewProj, vec4(inPosition, 1.0));
	float4 vWorldPos = mul(matWorld, vec4(inPosition, 1.0));
	float3 vWorldN = mul(matWorld, vec4(inNormal, 0.0)).xyz;
	
	float3 P = mul(matWorldView, vec4(inPosition, 1.0)).xyz;

	outTexCoord = inTexCoord;

	float4 diffuse_light = vAmbientColor + inColor1;
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor;
	diffuse_light += saturate(dot(vWorldN, -vSunDir.xyz)) * vSunColor;
	outColor0 = saturate(vMaterialColor * inColor0 * diffuse_light);

	//apply fog
	float d = length(P);
	outFog = get_fog_amount_new(d, vWorldPos.z);
}
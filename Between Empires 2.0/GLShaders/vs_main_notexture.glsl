
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
	
	outNormal = inNormal;
	outColor0 = inColor0.bgra * vMaterialColor;
	outColor1 = inColor1;
	outTexCoord = inTexCoord;
	
	//apply fog
	float3 P = mul(matWorldView, vec4(inPosition, 1.0)).xyz;
	float d = length(P);
	outFog = get_fog_amount(d);
}

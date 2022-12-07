
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;

varying float4 Pos;
varying float Fog;
varying float4 Color;
varying float2 Tex0;

void main()
{
	VS_OUTPUT_FONT VSOut;
	VSOut = vs_skybox(vec4(inPosition, 1.0), inColor0, inTexCoord);

	gl_Position = VSOut.Pos;
	Fog = VSOut.Fog;
	Color = VSOut.Color;
	Tex0 = VSOut.Tex0;
}

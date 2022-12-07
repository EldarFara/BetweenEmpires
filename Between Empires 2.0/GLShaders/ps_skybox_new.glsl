
varying float4 Pos;
varying float Fog;
varying float4 Color;
varying float2 Tex0;

void main()
{
	VS_OUTPUT_FONT VSOut;
	VSOut.Fog = Fog;
	VSOut.Color = Color;
	VSOut.Tex0 = Tex0;
	
	//skybox hdr-shader selection quick fix!
	gl_FragColor = ps_skybox_shading_new(true, VSOut).RGBColor; //we dont use non-hdr skybox textures on opengl mode!
}

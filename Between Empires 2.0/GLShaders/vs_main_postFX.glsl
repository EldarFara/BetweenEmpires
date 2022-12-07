
attribute vec3 inPosition;

varying float2 Tex;

void main()
{
	gl_Position = vec4(inPosition, 1.0);
	
	Tex = (float2(inPosition.x, inPosition.y) * 0.5 + 0.5)/* + g_HalfPixel_ViewportSizeInv.xy*/;
}

#version 130

uniform vec2 resolution;
uniform vec3[2000] sources;
uniform float[2000] offsets;
uniform float wavenumber;
uniform float scale;
uniform float color_range;
uniform int count;
uniform float z;
uniform bool xy_plane;
uniform bool xz_plane;

float colormap_red(float x) {
    if (x < 0.7) {
        return 4.0 * x - 1.5;
    } else {
        return -4.0 * x + 4.5;
    }
}

float colormap_green(float x) {
    if (x < 0.5) {
        return 4.0 * x - 0.5;
    } else {
        return -4.0 * x + 3.5;
    }
}

float colormap_blue(float x) {
    if (x < 0.3) {
       return 4.0 * x + 0.5;
    } else {
       return -4.0 * x + 2.5;
    }
}

vec4 colormap(float x) {
    float r = clamp(colormap_red(x), 0.0, 1.0);
    float g = clamp(colormap_green(x), 0.0, 1.0);
    float b = clamp(colormap_blue(x), 0.0, 1.0);
    return vec4(r, g, b, 1.0);
}


void main()
{ 
    vec3 pos;
    if (xy_plane) {
        pos = vec3((gl_FragCoord.xy / resolution.xy - vec2(0.5, 0.5)) * scale, z);
    }
    else if (xz_plane) {
        pos = vec3((gl_FragCoord.x / resolution.x - 0.5) * scale, z, (gl_FragCoord.y / resolution.y - 0.5) * scale);
    }
    else {
        pos = vec3(z, (gl_FragCoord.xy / resolution.xy - vec2(0.5, 0.5)) * scale);
    }
    float a=0;
    float b=0;
    for(int i=0; i<count; i++) {
        float dist = distance(pos, sources[i]);
        float phase = dist * wavenumber + offsets[i];
        a += 1 / dist * sin(phase);
        b += 1 / dist * cos(phase);
    }

    float val = sqrt(a*a + b*b)/color_range;
    if (val > 1.0) {
        val = 1.0;
    }

    gl_FragColor = colormap(val);
}

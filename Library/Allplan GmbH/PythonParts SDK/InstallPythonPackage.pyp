<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>allplan_gmbh\pythonparts_sdk\InstallPythonPackage.py</Name>
        <Title>Install Python Package</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page1</Name>
        <Text>pip</Text>

        <Parameter>
            <Name>PackageExpander</Name>
            <Text>PIP Package</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Row21</Name>
                <Text>PIP Package</Text>
                <ValueType>Row</ValueType>

                <Parameter>
                    <Name>package</Name>
                    <Text>PIP Package</Text>
                    <Value></Value>
                    <ValueType>String</ValueType>
                </Parameter>

                <Parameter>
                    <Name>Button21</Name>
                    <Text>Install</Text>
                    <EventId>2000</EventId>
                    <ValueType>Button</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>
        <Parameter>
            <Name>installLocation</Name>
            <Text>Target Location</Text>
            <Value>USR</Value>
            <ValueType>RadioButtonGroup</ValueType>

            <Parameter>
                <Name>USR</Name>
                <Text>USR</Text>
                <Value>USR</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
            <Parameter>
                <Name>STD</Name>
                <Text>STD</Text>
                <Value>STD</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
            <Parameter>
                <Name>ETC</Name>
                <Text>ETC</Text>
                <Value>ETC</Value>
                <ValueType>RadioButton</ValueType>
            </Parameter>
        </Parameter>

    </Page>
</Element>
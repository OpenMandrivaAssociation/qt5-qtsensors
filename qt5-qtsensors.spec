%define api %(echo %{version} |cut -d. -f1)
%define major %api
%define beta %{nil}

%define qtsensors %mklibname qt%{api}sensors %{major}
%define qtsensorsd %mklibname qt%{api}sensors -d

%define _qt5_prefix %{_libdir}/qt%{api}

Name:		qt5-qtsensors
Summary:	Qt5 - Sensors component
Version:	5.15.3
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qtsensors-everywhere-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	2
%define qttarballdir qtsensors-everywhere-opensource-src-%{version}
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
# From KDE
# [currently no patches required]
License:	LGPLv2 with exceptions or GPLv3 with exceptions
Url:		http://www.qt.io
BuildRequires:	qmake5 >= %{version}
BuildRequires:	pkgconfig(Qt5Core) >= %{version}
BuildRequires:	pkgconfig(Qt5DBus) >= %{version}
BuildRequires:	pkgconfig(Qt5Gui) >= %{version}
BuildRequires:	pkgconfig(Qt5Qml) >= %{version}
BuildRequires:	pkgconfig(Qt5Quick) >= %{version}
BuildRequires:	pkgconfig(Qt5Widgets) >= %{version}
BuildRequires:	pkgconfig(Qt5Test) >= %{version}
# For the Provides: generator
BuildRequires:	cmake >= 3.11.0-1

%description
The Qt Sensors API provides access to sensor hardware via QML and C++
interfaces.  The Qt Sensors API also provides a motion gesture recognition
API for devices.

#----------------------------------------------------------------------------

%package -n	%{qtsensors}
Summary:	Qt Sensors library
Group:		System/Libraries

%description -n %{qtsensors}
Qt Sensors library.

%files -n %{qtsensors}
%{_qt5_libdir}/libQt%{api}Sensors.so.%{major}*
%{_qt5_prefix}/qml/QtSensors
%{_qt5_plugindir}/sensorgestures
%{_qt5_plugindir}/sensors

#----------------------------------------------------------------------------

%package -n %{qtsensorsd}
Summary:	Development files for the QtSensors library
Group:		Development/KDE and Qt
Requires:	%{qtsensors} = %{EVRD}

%description -n %{qtsensorsd}
Development files for the QtSensors library.

%files -n %{qtsensorsd}
%{_qt5_includedir}/QtSensors
%{_qt5_libdir}/libQt%{api}Sensors.so
%{_qt5_libdir}/libQt%{api}Sensors.prl
%{_qt5_libdir}/cmake/Qt%{api}Sensors
%{_qt5_libdir}/pkgconfig/Qt%{api}Sensors.pc
%{_qt5_prefix}/mkspecs/modules/*.pri
%{_qt5_exampledir}/*

#----------------------------------------------------------------------------

%prep
%autosetup -n %(echo %qttarballdir|sed -e 's,-opensource,,') -p1
%{_qt5_prefix}/bin/syncqt.pl -version %{version}

%build
%qmake_qt5
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}
## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd
